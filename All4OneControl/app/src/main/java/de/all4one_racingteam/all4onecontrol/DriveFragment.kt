package de.all4one_racingteam.all4onecontrol

import android.app.Fragment
import android.os.Bundle
import android.util.Log
import android.view.LayoutInflater
import android.view.MotionEvent
import android.view.View
import android.view.ViewGroup
import android.widget.RelativeLayout
import kotlinx.android.synthetic.main.drive_layout.*
import java.nio.ByteBuffer
import java.nio.ByteOrder
import kotlin.math.atan2
import kotlin.math.roundToInt

class DriveFragment : Fragment() {

    override fun onCreateView(inflater: LayoutInflater?, container: ViewGroup?, savedInstanceState: Bundle?): View {
        if (inflater != null) {
            return inflater.inflate(R.layout.drive_layout, container, false)
        }
        return super.onCreateView(inflater, container, savedInstanceState)
    }

    var deltaX = 0
    var deltaY = 0

    override fun onViewCreated(view: View?, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        control_root.setOnTouchListener { view2: View, motionEvent: MotionEvent ->

            //val X = motionEvent.rawX.roundToInt()
            //val Y = motionEvent.rawY.roundToInt()
            val X = motionEvent.x.roundToInt()
            val Y = motionEvent.y.roundToInt()

            var layoutParams = image_thingy.layoutParams as RelativeLayout.LayoutParams
            layoutParams.leftMargin = X
            layoutParams.topMargin = Y
            layoutParams.rightMargin = -250
            layoutParams.bottomMargin = -250
            image_thingy.layoutParams = layoutParams

            var _x : Float = X.toFloat() / view2.width - 0.5f
            var _y : Float = -(Y.toFloat() / view2.height - 0.5f)

            var angle : Float = atan2(_x, _y)
            var speed : Float = _y * 2

            Log.d("Drive Fragment", "moved to X: $X; Y:$Y; _X:$_x; _Y:$_y")
            Log.d("Drive Fragment", "angle: $angle; speed: $speed")

            var byteBuffer = ByteBuffer.allocate(2 * 4)
            byteBuffer.order(ByteOrder.LITTLE_ENDIAN)
            byteBuffer.putFloat(angle)
            byteBuffer.putFloat(speed)

            var message: ByteArray = byteArrayOf('s'.toByte(), *byteBuffer.array())

            (activity.applicationContext as GlobalState).sendTcpMessage(message)
            return@setOnTouchListener true
        }

    }

}