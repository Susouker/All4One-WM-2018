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

class DriveFragment : ControlFragment() {

    override fun getTitle(): String {
        return getString(R.string.nav_drive_name)
    }

    override fun sendValues(relativeX: Float, relativeY: Float) {

        var angle : Float = relativeX * Math.PI.toFloat() / 2

        Log.d("Drive Fragment", "angle: $angle; speed: $relativeY")


        var steering = (relativeX * 128 + 128).toByte()
        var throttle = (relativeY * 128 + 128).toByte()

        var message: ByteArray = byteArrayOf('s'.toByte(), steering, throttle)

        (activity.applicationContext as GlobalState).sendTcpMessage(message)

    }

}