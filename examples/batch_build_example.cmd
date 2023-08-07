rem @echo off
set BUILDER=%HOMEDRIVE%%HOMEPATH%\Documents\GitHub\tkdecentsamplerlibrarybuilder\tkdecentsamplerlibrarybuilder.py
set PATH=%HOMEDRIVE%%HOMEPATH%\ANACON~1;%PATH%
set PYTHONHOME=%HOMEDRIVE%%HOMEPATH%\anaconda3
set PY=%PYTHONHOME%\pythonw.exe
call conda activate
%PY% %BUILDER% --do-build --input-folder .\160 --output-folder .\DS_broke_af_160_4x --cut-all-by-all --silencing-mode fast --start-note 24
%PY% %BUILDER% --do-build --input-folder .\160_1x --output-folder .\DS_broke_af_160_1x --cut-all-by-all --silencing-mode fast --start-note 36
%PY% %BUILDER% --do-build --input-folder .\160_2x --output-folder .\DS_broke_af_160_2x --cut-all-by-all --silencing-mode fast --start-note 0

%PY% %BUILDER% --do-build --input-folder .\165 --output-folder .\DS_broke_af_165_4x --cut-all-by-all --silencing-mode fast --start-note 24
%PY% %BUILDER% --do-build --input-folder .\165_1x --output-folder .\DS_broke_af_165_1x --cut-all-by-all --silencing-mode fast --start-note 36
%PY% %BUILDER% --do-build --input-folder .\165_2x --output-folder .\DS_broke_af_165_2x --cut-all-by-all --silencing-mode fast --start-note 0

%PY% %BUILDER% --do-build --input-folder .\170 --output-folder .\DS_broke_af_170_4x --cut-all-by-all --silencing-mode fast --start-note 24
%PY% %BUILDER% --do-build --input-folder .\170_1x --output-folder .\DS_broke_af_170_1x --cut-all-by-all --silencing-mode fast --start-note 36
%PY% %BUILDER% --do-build --input-folder .\170_2x --output-folder .\DS_broke_af_170_2x --cut-all-by-all --silencing-mode fast --start-note 0

%PY% %BUILDER% --do-build --input-folder .\172 --output-folder .\DS_broke_af_172_4x --cut-all-by-all --silencing-mode fast --start-note 24
%PY% %BUILDER% --do-build --input-folder .\172_1x --output-folder .\DS_broke_af_172_1x --cut-all-by-all --silencing-mode fast --start-note 36
%PY% %BUILDER% --do-build --input-folder .\172_2x --output-folder .\DS_broke_af_172_2x --cut-all-by-all --silencing-mode fast --start-note 0

%PY% %BUILDER% --do-build --input-folder .\174 --output-folder .\DS_broke_af_174_4x --cut-all-by-all --silencing-mode fast --start-note 24
%PY% %BUILDER% --do-build --input-folder .\174_1x --output-folder .\DS_broke_af_174_1x --cut-all-by-all --silencing-mode fast --start-note 36
%PY% %BUILDER% --do-build --input-folder .\174_2x --output-folder .\DS_broke_af_174_2x --cut-all-by-all --silencing-mode fast --start-note 0

%PY% %BUILDER% --do-build --input-folder .\175 --output-folder .\DS_broke_af_175_4x --cut-all-by-all --silencing-mode fast --start-note 24
%PY% %BUILDER% --do-build --input-folder .\175_1x --output-folder .\DS_broke_af_175_1x --cut-all-by-all --silencing-mode fast --start-note 36
%PY% %BUILDER% --do-build --input-folder .\175_2x --output-folder .\DS_broke_af_175_2x --cut-all-by-all --silencing-mode fast --start-note 0

%PY% %BUILDER% --do-build --input-folder .\176 --output-folder .\DS_broke_af_176_4x --cut-all-by-all --silencing-mode fast --start-note 24
%PY% %BUILDER% --do-build --input-folder .\176_1x --output-folder .\DS_broke_af_176_1x --cut-all-by-all --silencing-mode fast --start-note 36
%PY% %BUILDER% --do-build --input-folder .\176_2x --output-folder .\DS_broke_af_176_2x --cut-all-by-all --silencing-mode fast --start-note 0

%PY% %BUILDER% --do-build --input-folder .\178 --output-folder .\DS_broke_af_178_4x --cut-all-by-all --silencing-mode fast --start-note 24
%PY% %BUILDER% --do-build --input-folder .\178_1x --output-folder .\DS_broke_af_178_1x --cut-all-by-all --silencing-mode fast --start-note 36
%PY% %BUILDER% --do-build --input-folder .\178_2x --output-folder .\DS_broke_af_178_2x --cut-all-by-all --silencing-mode fast --start-note 0

%PY% %BUILDER% --do-build --input-folder .\180 --output-folder .\DS_broke_af_180_4x --cut-all-by-all --silencing-mode fast --start-note 24
%PY% %BUILDER% --do-build --input-folder .\180_1x --output-folder .\DS_broke_af_180_1x --cut-all-by-all --silencing-mode fast --start-note 36
%PY% %BUILDER% --do-build --input-folder .\180_2x --output-folder .\DS_broke_af_180_2x --cut-all-by-all --silencing-mode fast --start-note 0

