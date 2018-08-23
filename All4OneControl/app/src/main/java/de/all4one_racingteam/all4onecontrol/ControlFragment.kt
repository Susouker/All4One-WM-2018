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

open class ControlFragment : Fragment() {

    override fun onCreateView(inflater: LayoutInflater?, container: ViewGroup?, savedInstanceState: Bundle?): View {


        if (inflater != null) {
            var view = inflater.inflate(R.layout.drive_layout, container, false)
            return view
        }
        return super.onCreateView(inflater, container, savedInstanceState)
    }

    override fun onViewCreated(view: View?, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        header.text = getTitle()

        control_root.setOnTouchListener { view2: View, motionEvent: MotionEvent ->

            var x = motionEvent.x.roundToInt()
            var y = motionEvent.y.roundToInt()
            var relativeY = 0f

            var relativeX = Math.min(Math.max((x.toFloat() / view2.width - 0.5f) * 2, -1f), 1f)

            if (motionEvent.action == MotionEvent.ACTION_UP){
                //x = view2.width / 2
                y = view2.height / 2
            } else {
                 relativeY = Math.min(Math.max((y.toFloat() / view2.height - 0.5f) * -2, -1f), 1f)
            }

            var layoutParams = image_thingy.layoutParams as RelativeLayout.LayoutParams
            layoutParams.leftMargin = x - image_thingy.width / 2
            layoutParams.topMargin = y - image_thingy.height / 2
            layoutParams.rightMargin = -250
            layoutParams.bottomMargin = -250
            layoutParams.removeRule(RelativeLayout.CENTER_IN_PARENT)
            image_thingy.layoutParams = layoutParams

            Log.d("Control Fragment", "moved to X: $x; Y:$y; _X:$relativeX; _Y:$relativeY")
            sendValues(relativeX, relativeY)
            return@setOnTouchListener true
        }

    }

    protected open fun sendValues(relativeX: Float, relativeY: Float){}
    protected open fun getTitle() : String { return "" }

}