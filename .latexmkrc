# references.bib is in src/; pdflatex runs in src/{proposal,thesis}, BibTeX runs in build/
ensure_path( 'ENV', 'BIBINPUTS', '../src//:..//:' );
$bibtex = 'BIBINPUTS=../src//:../..//:$ENV{BIBINPUTS} bibtex %O %B';
