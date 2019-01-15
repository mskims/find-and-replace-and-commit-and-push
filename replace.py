import os
import pathlib
import sys
import uuid

from git import Repo

from utils import YES

search = sys.argv[1].encode()
replace = sys.argv[2].encode()

repository_urls = [
    'git@github.com:ridi/search-api.git',
    'git@github.com:ridi/super-api.git',
    'git@github.com:ridi/user-api.git',
    'git@github.com:ridi/cms-api.git',
]

PUSH_TO_MASTER = False

repos = []
pathlib.Path('./_workspace').mkdir(parents=True, exist_ok=True)
for repo_url in repository_urls:
    print('Initializing', repo_url, '...')

    if pathlib.Path('./_workspace/' + repo_url).exists():
        repo = Repo('./_workspace/' + repo_url)
        repo.git.checkout('master')
        repo.head.reset('origin/HEAD', index=True, working_tree=True)
        repo.remotes.origin.pull()
    else:
        repo = Repo.clone_from(repo_url, './_workspace/' + repo_url)

    repos.append(repo)
    for item in repo.head.commit.tree.traverse():
        if item.type is not 'blob':
            continue

        with open(item.abspath, 'rb') as file:
            filedata = file.read()

        if filedata.find(search) is -1:
            continue

        replaced_filedata = filedata.replace(search, replace)

        with open(item.abspath, 'wb') as file:
            file.write(replaced_filedata)

for repo in repos:
    index = repo.index

    diffs = index.diff(None, create_patch=True).iter_change_type('M')

    dirty = False
    for diff in diffs:
        print(diff)
        print('Add it to staged changes (y/n)? ', end='')
        choice = input().lower()
        if choice not in YES:
            continue

        index.add([os.path.join(repo.working_tree_dir, diff.b_blob.path)])
        dirty = True

    repo.dirty = dirty
    if not dirty:
        continue

    if not PUSH_TO_MASTER:
        new_branch = repo.create_head('refac/replace-' + str(uuid.uuid4())[1:5])
        new_branch.checkout()

    index.commit('Replace {} with {}'.format(
        search.decode(), replace.decode()))

print('Affected files:')
for repo in repos:
    if not repo.dirty:
        continue
    print('  ' + list(repo.remotes.origin.urls)[0] + ':')
    stats = repo.head.commit.stats
    for path in stats.files.keys():
        print('    ' + path)

print('Push (y/n)? ', end='')
choice = input().lower()
if choice not in YES:
    raise SystemExit()

for repo in repos:
    if not repo.dirty:
        continue
    repo.remotes.origin.push()

print('Done!')
