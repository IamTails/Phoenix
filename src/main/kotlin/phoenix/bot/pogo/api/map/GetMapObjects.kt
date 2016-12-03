package phoenix.bot.pogo.api.map

import phoenix.bot.pogo.api.PoGoApi
import phoenix.bot.pogo.api.cache.Map
import phoenix.bot.pogo.api.request.GetMapObjects

class GetMapObjects(poGoApi: PoGoApi, width: Int = 3) : GetMapObjects() {
    init {
        Map.getCellIds(poGoApi.latitude, poGoApi.longitude, width).forEach {
            this.withCellId(it)
            val oldCell = poGoApi.map.mapCells.get(it)
            if (oldCell == null || oldCell.lastUpdated == 0L) {
                this.withSinceTimestampMs(0)
                //println("Requesting cell $it with lastUpdated timestampSince $timestampSince")
            } else {
                this.withSinceTimestampMs(oldCell.lastUpdated)
                //println("Requesting cell $it with lastUpdated oldValue ${oldCell.lastUpdated}")
            }
        }
    }
}