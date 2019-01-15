# find-and-replace-and-commit-and-push

각 저장소에 있는 특정 문자열을 찾아 변경하고, 커밋과 푸시까지 자동으로 수행해주는 스크립트입니다.

## Usage

```bash
# replace.py
repository_urls = [
    'git@github.com:ridi/user-api.git',
    'git@github.com:ridi/search-api.git',
]

$ python replace.py 10.12.151.12 db.ridi.io
```

## Todo

- [ ] Pull Request 자동 생성
- [ ] `sys.arg`에서 `repository_urls` 가져오기
- [ ] `sys.arg`에서 `PUSH_TO_MASTER` 가져오기

## License

MIT
