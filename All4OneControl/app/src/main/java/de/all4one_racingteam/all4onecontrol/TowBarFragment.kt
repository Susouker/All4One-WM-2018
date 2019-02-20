package de.all4one_racingteam.all4onecontrol

import android.app.Fragment
import android.os.Bundle
import android.util.Log
import android.view.*
import android.widget.RelativeLayout
import kotlinx.android.synthetic.main.drive_layout.*
import org.jetbrains.anko.centerInParent
import org.jetbrains.anko.db.FloatParser
import java.nio.ByteBuffer
import java.nio.ByteOrder
import kotlin.math.atan2
import kotlin.math.roundToInt

class TowBarFragment : ControlFragment() {
    override fun getTitle(): String {
        return getString(R.string.nav_towbar_name)
    }

    override fun sendValues(relativeX: Float, relativeY: Float) {

        var position : Float = relativeX / 2 + 0.5f


        Log.d("Tow Bar Fragment", "position $position")
/*
        var byteBuffer = ByteBuffer.allocate(1 * 4)
        byteBuffer.order(ByteOrder.LITTLE_ENDIAN)
        byteBuffer.putFloat(position)
*/
        var tbPos = (position * 256).toByte()
        var message: ByteArray = byteArrayOf('b'.toByte(), tbPos)

        (activity.applicationContext as GlobalState).sendTcpMessage(message)

    }

}