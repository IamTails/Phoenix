/**
 * Pokemon Go Bot  Copyright (C) 2016  PokemonGoBot-authors (see authors.md for more information)
 * This program comes with ABSOLUTELY NO WARRANTY;
 * This is free software, and you are welcome to redistribute it under certain conditions.
 *
 * For more information, refer to the LICENSE file in this repositories root directory
 */

package phoenix.bot.pogo.nRnMK9r.util.data

import phoenix.bot.pogo.api.cache.BagPokemon
import phoenix.bot.pogo.nRnMK9r.util.pokemon.eggKmWalked
import phoenix.bot.pogo.nRnMK9r.util.pokemon.incubated

data class EggData(
        var isIncubate: Boolean? = null,
        var kmWalked: Double? = null,
        var kmTarget: Double? = null
) {
    fun buildFromEggPokemon(egg: BagPokemon): EggData {
        this.isIncubate = egg.pokemonData.incubated
        this.kmWalked = egg.pokemonData.eggKmWalked(egg.poGoApi)
        this.kmTarget = egg.pokemonData.eggKmWalkedTarget

        return this
    }
}
