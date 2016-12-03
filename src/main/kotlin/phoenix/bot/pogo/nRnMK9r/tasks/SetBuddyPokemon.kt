/**
 * Pokemon Go Bot  Copyright (C) 2016  PokemonGoBot-authors (see authors.md for more information)
 * This program comes with ABSOLUTELY NO WARRANTY;
 * This is free software, and you are welcome to redistribute it under certain conditions.
 *
 * For more information, refer to the LICENSE file in this repositories root directory
 */

package phoenix.bot.pogo.nRnMK9r.tasks

import POGOProtos.Networking.Responses.SetBuddyPokemonResponseOuterClass
import phoenix.bot.pogo.api.request.SetBuddyPokemon
import phoenix.bot.pogo.nRnMK9r.Bot
import phoenix.bot.pogo.nRnMK9r.Context
import phoenix.bot.pogo.nRnMK9r.Settings
import phoenix.bot.pogo.nRnMK9r.Task
import phoenix.bot.pogo.nRnMK9r.util.Log


class SetBuddyPokemon : Task {
    override fun run(bot: Bot, ctx: Context, settings: Settings) {
        var replaceBuddy = false
        val currentBuddy = if (ctx.api.playerData.hasBuddyPokemon()) {
            ctx.api.inventory.pokemon[ctx.api.playerData.buddyPokemon.id]
        } else {
            null
        }
        if (currentBuddy != null) {
            if (settings.buddyPokemon.toUpperCase().trim() != currentBuddy.pokemonData.pokemonId.name) {
                replaceBuddy = true
            }
        } else {
            replaceBuddy = true
        }
        if (replaceBuddy) {
            val desiredBuddies = ctx.api.inventory.pokemon.filter {
                it.value.pokemonData.pokemonId.name == settings.buddyPokemon.toUpperCase().trim()
            }.toList()
            if (desiredBuddies.size > 0) {
                val setBuddyRequest = SetBuddyPokemon().withPokemonId(desiredBuddies[0].first)
                val response = ctx.api.queueRequest(setBuddyRequest).toBlocking().first().response
                if (response.result == SetBuddyPokemonResponseOuterClass.SetBuddyPokemonResponse.Result.SUCCESS) {
                    Log.green("Updated Buddy Pokemon to ${ctx.api.inventory.pokemon[response.updatedBuddy.id]?.pokemonData?.pokemonId?.name}")
                }
            }
        }
    }
}
