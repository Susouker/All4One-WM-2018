package de.all4one_racingteam.all4onecontrol

import android.app.Fragment
import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Toast
import kotlinx.android.synthetic.main.vgc_select_layout.*

class RoutineSelectFragment : Fragment() {

    override fun onCreateView(inflater: LayoutInflater?, container: ViewGroup?, savedInstanceState: Bundle?): View {
        if (inflater != null) {
            return inflater.inflate(R.layout.routine_select_layout, container, false)
        }


        return super.onCreateView(inflater, container, savedInstanceState)
    }

    override fun onViewCreated(view: View?, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        button1.setOnClickListener { _ : View ->
            Toast.makeText(activity.applicationContext, "Starting Routine Steering Demo", Toast.LENGTH_LONG).show()
            val message: ByteArray = byteArrayOf('d'.toByte(), 'D'.toByte())
            (activity.applicationContext as GlobalState).sendTcpMessage(message)
        }
    }
}