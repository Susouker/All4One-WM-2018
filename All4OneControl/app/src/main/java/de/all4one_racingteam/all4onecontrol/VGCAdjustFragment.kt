package de.all4one_racingteam.all4onecontrol

import android.app.Fragment
import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.SeekBar
import android.widget.Toast
import kotlinx.android.synthetic.main.vgc_adjust_layout.*
import kotlinx.android.synthetic.main.vgc_select_layout.*

class VGCAdjustFragment : Fragment() {

    var tracking = false


    override fun onCreateView(inflater: LayoutInflater?, container: ViewGroup?, savedInstanceState: Bundle?): View {
        if (inflater != null) {
            return inflater.inflate(R.layout.vgc_adjust_layout, container, false)
        }

        seekBar_vgc_pos.max = 256

        return super.onCreateView(inflater, container, savedInstanceState)
    }

    override fun onViewCreated(view: View?, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        button_fast_dec.setOnClickListener { _: View ->
            sendAdjustment(-10)
        }
        button_slow_dec.setOnClickListener { _: View ->
            sendAdjustment(-1)
        }
        button_slow_inc.setOnClickListener { _: View ->
            sendAdjustment(1)
        }
        button_fast_inc.setOnClickListener { _: View ->
            sendAdjustment(10)
        }
        seekBar_vgc_pos.setOnSeekBarChangeListener(object : SeekBar.OnSeekBarChangeListener {
            override fun onStopTrackingTouch(p0: SeekBar?) {
                tracking = false
                if (p0 != null) {
                    sendManualVGCHeight(p0.progress.toByte())
                }
            }

            override fun onStartTrackingTouch(p0: SeekBar?) {
                tracking = true
            }

            override fun onProgressChanged(p0: SeekBar?, p1: Int, p2: Boolean) {
                if (!tracking)
                    sendManualVGCHeight(p1.toByte())
            }
        })
    }

    private fun sendAdjustment(value: Int) {

        var adjustMin = switch_min_max.isChecked
        var wheel = wheel_select.selectedItemId.toInt()
        var wheelName = wheel_select.selectedItem.toString()

        Toast.makeText(activity.applicationContext, "Von Rad $wheelName die Seite $adjustMin um $value angepasst", Toast.LENGTH_SHORT).show()
        var valueToSend: Int = value * 8 + wheel
        if (adjustMin)
            valueToSend += 4

        val message: ByteArray = byteArrayOf('W'.toByte(), valueToSend.toByte())
        (activity.applicationContext as GlobalState).sendTcpMessage(message)

    }

    private fun sendManualVGCHeight(height: Byte) {


        var message: ByteArray = byteArrayOf('H'.toByte(), 'M'.toByte(), height)
        (activity.applicationContext as GlobalState).sendTcpMessage(message)
    }
}