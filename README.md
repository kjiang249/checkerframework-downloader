# checkerframework-downloader
# Overview
This downloader can be used to download all the releases at https://github.com/eisop/
checker-framework/releases.
# Usage
The request.py is used to download all releases.
The clean.py clean up anything under folder "cf" and "afu" created by request.py
# Expected outputs
```bash
downloader folder
├── afu
    └──#releases-eisop#.zip
    └──#releases-eisop#(folder)
├── cf
│   └── checker-framework-#releases-eisop#.zip
│   └── checker-framework-#releases(folder)
│       └──annotation-file-utilites(symlink)
│       └──api(folder)
│       └──checker(folder)
│       └──docs(folder)
│       └──manual(symlink)
│       └──tutorial(symlink)
│       └──CHANGELOG.md(symlink)
│       └──checker-framework-#releases.zip(symlink)
│       └──index.html
│       └──LICENSE.txt
├── clean.py
└── request.py
```