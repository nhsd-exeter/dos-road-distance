# API Document generation

## Prerequisites

* Install spectacle-docs

    `npm install -g spectacle-doc`

* Clone the swagger-codegen repository

    `git clone https://github.com/swagger-api/swagger-codegen.git`

## Generate documentation

The templates required to generate documentation are located in:

  swagger-codegen/modules/swagger-codegen/src/main/resources/htmlDocs2

`swagger-codegen generate -i <path-to-yaml-file> -l html2 -o <output-location> -t <template-location>`
