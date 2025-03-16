(configuration-settings)=
# Configuration Settings

```json
{
    "filter": "shapescape_world_settings",
    "settings": {
        "level_dat_path": "../level.dat",
        "release_config_path": "../pack/release_config.json"
    }
}
```

- `level_dat_path: str` - the path to the `level.dat` file. By default relative to the `config.json` file of the project (see `paths_relative_to_config_json`)
- `release_config_path: str` - the path to the `release_config.json` file (see {ref}`Usage<usage>` section for more details). By default relative to the `config.json` file of the project (see `paths_relative_to_config_json`)
- `paths_relative_to_config_json: bool = True` - optional, default `True`. If `True`, the paths are relative to the `config.json` file. If `False`, the paths are relative to the current working directory during the execution of the filter (the `tmp` file with `RP`, `BP` and `data` folders)
