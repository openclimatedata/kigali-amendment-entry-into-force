Data Package with Ratification Status of the Kigali Amendment to the Montreal Protocol

[![Weekly Update](https://github.com/openclimatedata/kigali-amendment-entry-into-force/workflows/Weekly%20Update/badge.svg)](https://github.com/openclimatedata/kigali-amendment-entry-into-force/actions)

## Data

The dataset contains dates of Acceptance, Ratification, or Approval of the
Kigali Amendment to the Montreal Protocol and makes it available as a simple CSV file.
See the [UNFCCC page on the Ratification Status](https://treaties.un.org/Pages/ViewDetails.aspx?src=TREATY&mtdsg_no=XXVII-2-f&chapter=27&clang=_en) for
further information.
Source for this dataset is the XML version in the official [UN Treaty
Collection](https://treaties.un.org/doc/Publication/MTDSG/Volume%20II/Chapter%20XXVII/XXVII-2-f.en.xml)


## Preparation

The `Makefile` requires Python3 and will automatically install its dependencies
into a Virtualenv when run with

```shell
make
```

Running `make` will also update the repo, then fetch and update the dataset. The
download and extraction is done in `script/process.py`.
