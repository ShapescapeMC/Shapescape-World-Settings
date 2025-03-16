(usage)=
# Usage

Before running the filter you have to set up the `release_config.json` file. Everything that the filter does is based on the values in this file.

## The release_config.json file

The `release_config.json` file uses the following properties:

- `product_name: str` - the name of the product. The filter renames the world to this value.
- `settings->multiplayer: bool` - Enables/Disables multiplayer. Internally it controls two properties. The checkbox for the multiplayer and the "Microsoft Account Settings" dropdown. If the value is "true", the checkbox is checked and the dropdown is set to "Friends of Friends". If the value is "false", the checkbox is unchecked and the dropdown is set to "Invite Only".
- `settings->cheats: bool` - Enables/Disables cheats.
- `settings->send_command_feedback: bool` - Enables/Disables the sendcommandfeedback gamerule.
- `settings->commandblockoutput: bool` - Enables/Disables the commandblockoutput gamerule.
- `settings->do_day_light_cycle: bool` - Enables/Disables the doDayLightCycle gamerule.
- `settings->do_mob_spawning: bool` - Enables/Disables the doMobSpawning gamerule.
- `settings->difficulty: Literal['peaceful', 'easy', 'normal', 'hard']` - Sets the difficulty of the world. The value must be one of the following: `peaceful`, `easy`, `normal`, `hard`.
- `settings->defaultGamemode: Literal['survival', 'creative', 'adventure']` - Sets the default gamemode of the world. The value must be one of the following: `survival`, `creative`, `adventure`.

All other properties are ignored.

### Example:

```json
{
	"product_creator": "Shapescape",
	"product_name": "Level Dat Updater Test",
	"product_key": "YWN",
	"product_description": "By Shapescape",
	"settings": {
		"multiplayer": true,
		"cheats": false,
		"sendCommandFeedback": false,
		"commandBlockOutput": false,
		"doDayLightCycle": true,
		"doMobSpawning": true,
		"difficulty": "normal"
	}
}
```
