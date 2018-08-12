package de.all4one_racingteam.all4onecontrol

import android.app.Fragment
import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup

class SelectFragment : Fragment() {

    override fun onCreateView(inflater: LayoutInflater?, container: ViewGroup?, savedInstanceState: Bundle?): View {
        if (inflater != null) {
            return inflater.inflate(R.layout.select_layout, container, false)
        }


        return super.onCreateView(inflater, container, savedInstanceState)
    }
}