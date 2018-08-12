package de.all4one_racingteam.all4onecontrol

import android.app.Fragment
import android.os.Bundle
import android.os.Debug
import android.support.design.widget.Snackbar
import android.util.Log
import android.view.LayoutInflater
import android.view.MotionEvent
import android.view.View
import android.view.ViewGroup
import android.widget.RelativeLayout
import kotlinx.android.synthetic.main.drive_layout.*
import kotlinx.android.synthetic.main.options_layout.*
import kotlin.math.roundToInt

class OptionsFragment : Fragment() {

    override fun onCreateView(inflater: LayoutInflater?, container: ViewGroup?, savedInstanceState: Bundle?): View {

        if (inflater != null) {
            return inflater.inflate(R.layout.options_layout, container, false)
        }
        return super.onCreateView(inflater, container, savedInstanceState)
    }

    override fun onViewCreated(view: View?, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        checkBoxLight.setOnClickListener { _: View ->
            var message: ByteArray = byteArrayOf('t'.toByte(), 'L'.toByte(), 0)
            if(checkBoxLight.isChecked)
                message[2] = 1

            (activity.applicationContext as GlobalState).sendTcpMessage(message)
        }
    }

}