package de.all4one_racingteam.all4onecontrol

import android.support.v7.app.AppCompatActivity
import android.os.Bundle

class SettingsActivity : AppCompatActivity() {

    companion object {
        var hostnameKey = "hostname"
        var portKey = "port"
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        supportFragmentManager.beginTransaction().replace(android.R.id.content, SettingsFragment()).commit()
    }
}
