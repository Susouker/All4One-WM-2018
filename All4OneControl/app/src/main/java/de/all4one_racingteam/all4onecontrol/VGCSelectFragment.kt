package de.all4one_racingteam.all4onecontrol

import android.app.Fragment
import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Toast
import kotlinx.android.synthetic.main.vgc_select_layout.*

class VGCSelectFragment : Fragment() {

    override fun onCreateView(inflater: LayoutInflater?, container: ViewGroup?, savedInstanceState: Bundle?): View {
        if (inflater != null) {
            return inflater.inflate(R.layout.vgc_select_layout, container, false)
        }


        return super.onCreateView(inflater, container, savedInstanceState)
    }

    override fun onViewCreated(view: View?, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        button1.setOnClickListener { _: View ->
            setVGCMode('F')
        }

        button2.setOnClickListener { _: View ->
            setVGCMode('A')
        }

        button3.setOnClickListener { _: View ->
            setVGCMode('P')
        }
    }

    private  fun setVGCMode(mode : Char){
        Toast.makeText(activity.applicationContext, "Setting VGC Mode to $mode", Toast.LENGTH_SHORT).show()
        val message: ByteArray = byteArrayOf('v'.toByte(), mode.toByte())
        (activity.applicationContext as GlobalState).sendTcpMessage(message)

    }
}