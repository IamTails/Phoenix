/**
 * Pokemon Go Bot  Copyright (C) 2016  PokemonGoBot-authors (see authors.md for more information)
 * This program comes with ABSOLUTELY NO WARRANTY;
 * This is free software, and you are welcome to redistribute it under certain conditions.
 *
 * For more information, refer to the LICENSE file in this repositories root directory
 */

package hydra.bot.pogo.qk9pBEF.tasks

import com.pokegoapi.api.map.fort.Pokestop
import hydra.bot.pogo.qk9pBEF.Bot
import hydra.bot.pogo.qk9pBEF.Context
import hydra.bot.pogo.qk9pBEF.Settings
import hydra.bot.pogo.qk9pBEF.Task
import hydra.bot.pogo.qk9pBEF.util.Log

class BypassSoftban(val pokestop: Pokestop) : Task {
    override fun run(bot: Bot, ctx: Context, settings: Settings) {
        repeat(settings.banSpinCount) { i ->
            pokestop.loot()

            if ((i + 1) % 10 == 0)
                Log.yellow("${i + 1}/${settings.banSpinCount}")
        }
    }
}