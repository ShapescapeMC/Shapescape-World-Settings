(installation)=
# Installation

## Steps

### 1. Install the filter
Use the following command

```
regolith install shapescape_world_settings
```

You can alternatively use this command:
```
regolith install github.com/ShapescapeMC/Shapescape-World-Settings/shapescape_world_settings
```

### 2. Add filter to a profile
Add the filter to the `filters` list in the `config.json` file of the Regolith project and add the settings:

```json
{
    "filter": "shapescape_world_settings",
    "settings": {
        "level_dat_path": "../level.dat",
        "release_config_path": "../pack/release_config.json"
    }
}
```

```{note}
The configuration settings are explained in the {ref}`Configuration Settings <configuration-settings>` section.
```