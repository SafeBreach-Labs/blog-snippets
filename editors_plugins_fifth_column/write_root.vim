if !has('python') && !has('python3')
    finish
endif

function! RootWrite()
    If has('python')
        pyfile ~/.vim/plugin/write_root_file.py
    else
        py3file ~/.vim/plugin/write_root_file.py
    endif
endfunc

call RootWrite()
