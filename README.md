## googlecli

A command line google search tool inspired by cli-google, with some improvements.

## Install
```
pip install 'git+https://github.com/ppwwyyxx/googlecli.git'
```

## Usage
```
usage: google [-s START] [-n NUMBER] [-l LANGUAGE] [--no-color] [-o] [-r] query

optional arguments:
  -s START, --start START
                        start at the Nth result
  -n NUMBER, --number NUMBER
                        show N results
  -l LANGUAGE, --language LANGUAGE
                        search by language
  --no-color            disable color output
  -o, --open            open the first result with browser (feeling lucky)
  -r, --reverse         output in reversed order, to work with URL selecter in tmux/urxv
```

## Good Practice
Use `alias gg='google -r'` to have reversed output, and use a console-based URL selecter such as
[tmux-url-select](https://github.com/dequis/tmux-url-select)
or [urxvt-url-select](https://github.com/muennich/urxvt-perls), to open any url.

Use `alias gl='google -o'` when you're feeling lucky.

## Screenshot
![screen](https://github.com/ppwwyyxx/googlecli/raw/master/screenshot.gif)
