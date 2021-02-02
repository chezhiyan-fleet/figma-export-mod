# Figma Export

Usually app developers export Figma components (icons, decorations, etc) and import them to IDE manually. The goal of this project is to make this job easier.

Exports components from any Figma document and saves them to files that can be easily imported to other applications.

Allows to export your Figma components as:

- Image files (```png```, ```jpg```, ```svg```).

## Installation

- Set an environment variable ```FIGMA_ACCESS_TOKEN``` to your [personal access token](https://www.figma.com/developers/api#access-tokens).


## Usage examples

Export all components as PNG files:

```
$ figma_export png DOCUMENT_ID
```

Node Ids are static for now and are defined in "FigmaClient.py". Replace them with the node-id you are trying to export



