package phoenix.bot.pogo.api.cache

import POGOProtos.Map.Fort.FortDataOuterClass
import phoenix.bot.pogo.api.PoGoApi

class Pokestop(poGoApi: PoGoApi, rawData: FortDataOuterClass.FortData) : Fort(poGoApi, rawData) {
    var cooldownCompleteTimestampMs = fortData.cooldownCompleteTimestampMs
}