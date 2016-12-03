package phoenix.bot.pogo.api.util

class SystemTimeImpl : Time {
    override fun currentTimeMillis(): Long {
        return System.currentTimeMillis()
    }
}
