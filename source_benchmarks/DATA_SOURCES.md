# Dataset attribution and snapshot identity



Original datasets are distributed by UCI under CC BY 4.0: https://creativecommons.org/licenses/by/4.0/. Attribution is retained here; no endorsement is implied. The ZIP files under raw/ are unchanged source downloads. Derived scores and splits result from the transformations documented in each phase protocol and runner.



## ctg

Source/DOI: https://doi.org/10.24432/C51S4N

Citation: Campos D, Bernardes J. Cardiotocography (2000).

UCI public source; CC BY 4.0. Snapshot acquired for the 7 October 2026 phase; no pinned upstream release number.

Target: NSP=3; negative: NSP=1 or 2. Features: 21 numbered diagnostic features only; no CLASS or morphology indicators.

SHA-256: ba2853564e282779907242b7bd8a83265d9fc4e79bb008573967daa16677bb6c



## wdbc

Source/DOI: https://doi.org/10.24432/C5DW2B

Citation: Wolberg W, Mangasarian O, Street N, Street W. Breast Cancer Wisconsin (Diagnostic) (1993).

UCI public source; CC BY 4.0. Snapshot acquired for the 7 October 2026 phase; no pinned upstream release number.

Target: M; negative: B. Features: 30 measurements; ID excluded.

SHA-256: bc154869ef13f753f9e2b5a17e248cfe1ba4b6721db7c4da9f4880e40b05d3af



## climate

Citation: Lucas et al. (2013). DOI: 10.24432/C5HG71

Source: https://archive.ics.uci.edu/dataset/252/climate+model+simulation+crashes

Download: https://archive.ics.uci.edu/static/public/252/climate+model+simulation+crashes.zip

License: CC BY 4.0; access: Public, no authentication. Retrieved: 2026-10-16. UCI download snapshot; repository provides no pinned release number.

Positive class: outcome=0 (failure). Transformations: columns 3-20; exclude study/run IDs; see frozen protocol and runner for cleaning/imputation.

SHA-256: fe8c0c2b79d1beedf31fbca2db8a97cec3c1b773ee29ed3357a2ff1dc8dd12d0



## seismic

Citation: Sikora and Wrobel (2010). DOI: 10.24432/C5W902

Source: https://archive.ics.uci.edu/dataset/266/seismic+bumps

Download: https://archive.ics.uci.edu/static/public/266/seismic+bumps.zip

License: CC BY 4.0; access: Public, no authentication. Retrieved: 2026-10-16. UCI download snapshot; repository provides no pinned release number.

Positive class: class=1 (next-shift hazardous event). Transformations: 18 predictors; categorical seismic,seismoacoustic,shift,ghazard; see frozen protocol and runner for cleaning/imputation.

SHA-256: 0acf2dc3a5df784ec77d1b8bfc4f7754ca88d0278828ce0684e4b1f73e04c37b



## blood

Citation: Yeh (2008). DOI: 10.24432/C5GS39

Source: https://archive.ics.uci.edu/dataset/176/blood+transfusion+service+center

Download: https://archive.ics.uci.edu/static/public/176/blood+transfusion+service+center.zip

License: CC BY 4.0; access: Public, no authentication. Retrieved: 2026-10-16. UCI download snapshot; repository provides no pinned release number.

Positive class: donation in March 2007=1. Transformations: four RFM/T predictors; see frozen protocol and runner for cleaning/imputation.

SHA-256: 95c39e2e05972bdc8a9c6fe521184cc8284578885d5b3e0c553d3f7dd9543221



## mammographic

Citation: Elter (2007). DOI: 10.24432/C53K6Z

Source: https://archive.ics.uci.edu/dataset/161/mammographic+mass

Download: https://archive.ics.uci.edu/static/public/161/mammographic+mass.zip

License: CC BY 4.0; access: Public, no authentication. Retrieved: 2026-10-16. UCI download snapshot; repository provides no pinned release number.

Positive class: Severity=1 malignant. Transformations: Age,Shape,Margin,Density; exclude BI-RADS; Shape/Margin categorical; see frozen protocol and runner for cleaning/imputation.

SHA-256: 4c5158166aa7f1503e14d95be4c95fe66a734474f614441ede226314b93db6e7



## spambase

Citation: Hopkins et al. (1999). DOI: 10.24432/C53G6X

Source: https://archive.ics.uci.edu/dataset/94/spambase

Download: https://archive.ics.uci.edu/static/public/94/spambase.zip

License: CC BY 4.0; access: Public, no authentication. Retrieved: 2026-10-16. UCI download snapshot; repository provides no pinned release number.

Positive class: last column=1 spam. Transformations: 57 numerical features; see frozen protocol and runner for cleaning/imputation.

SHA-256: 813ac1df8effac70463c09c9c4b11e8803eefcab54771af66150852bcdcd1636

