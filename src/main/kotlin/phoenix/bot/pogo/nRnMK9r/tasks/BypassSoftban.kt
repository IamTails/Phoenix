/**
 * Pokemon Go Bot  Copyright (C) 2016  PokemonGoBot-authors (see authors.md for more information)
 * This program comes with ABSOLUTELY NO WARRANTY;
 * This is free software, and you are welcome to redistribute it under certain conditions.
 *
 * For more information, refer to the LICENSE file in this repositories root directory
 */

package phoenix.bot.pogo.nRnMK9r.tasks

import phoenix.bot.pogo.api.cache.Pokestop
import phoenix.bot.pogo.nRnMK9r.Bot
import phoenix.bot.pogo.nRnMK9r.Context
import phoenix.bot.pogo.nRnMK9r.Settings
import phoenix.bot.pogo.nRnMK9r.Task
import phoenix.bot.pogo.nRnMK9r.util.Log
import phoenix.bot.pogo.nRnMK9r.util.map.loot

class BypassSoftban(val pokestop: Pokestop) : Task {
    override fun run(bot: Bot, ctx: Context, settings: Settings) {
        repeat(settings.banSpinCount) { i ->
            pokestop.loot()

            if ((i + 1) % 10 == 0)
                Log.yellow("${i + 1}/${settings.banSpinCount}")
        }
    }
}
