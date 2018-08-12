package de.all4one_racingteam.all4onecontrol

import android.os.Bundle
import android.support.design.widget.Snackbar
import android.support.design.widget.NavigationView
import android.support.v4.view.GravityCompat
import android.support.v7.app.ActionBarDrawerToggle
import android.support.v7.app.AppCompatActivity
import android.view.Menu
import android.view.MenuItem
import kotlinx.android.synthetic.main.activity_main.*
import kotlinx.android.synthetic.main.app_bar_main.*

class MainActivity : AppCompatActivity(), NavigationView.OnNavigationItemSelectedListener {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        setSupportActionBar(toolbar)

        fab.setOnClickListener { view ->
            Snackbar.make(view, "Replace with your own action", Snackbar.LENGTH_LONG)
                    .setAction("Action", null).show()
        }

        val toggle = ActionBarDrawerToggle(this, drawer_layout, toolbar,  R.string.navigation_drawer_close, R.string.navigation_drawer_close)
        drawer_layout.addDrawerListener(toggle)
        toggle.syncState()

        nav_view.setNavigationItemSelectedListener(this)

        nav_view.setCheckedItem(R.id.nav_drive_layout)
        fragmentManager.beginTransaction().replace(R.id.content_frame, DriveFragment()).commit()
    }

    override fun onBackPressed() {
        if (drawer_layout.isDrawerOpen(GravityCompat.START)) {
            drawer_layout.closeDrawer(GravityCompat.START)
        } else {
            super.onBackPressed()
        }
    }

    override fun onCreateOptionsMenu(menu: Menu): Boolean {
        menuInflater.inflate(R.menu.main, menu)
        return true
    }

    override fun onPrepareOptionsMenu(menu: Menu?): Boolean {
        if ((applicationContext as GlobalState).isTcpClientConnected()) {
            menu!!.getItem(1).isEnabled = false
            menu.getItem(2).isEnabled = true
        } else {
            menu!!.getItem(1).isEnabled = true
            menu.getItem(2).isEnabled = false
        }

        return super.onPrepareOptionsMenu(menu)
    }

    override fun onOptionsItemSelected(item: MenuItem): Boolean {
        return when (item.itemId) {
            R.id.action_settings -> {
                true
            }
            R.id.action_connect -> {
                (applicationContext as GlobalState).connectTcpClient()
                true
            }
            R.id.action_disconnect -> {
                (applicationContext as GlobalState).disconnectTcpClient()
                true
            }
            else -> super.onOptionsItemSelected(item)
        }
    }

    override fun onNavigationItemSelected(item: MenuItem): Boolean {
        var fragmentManager = fragmentManager

        when (item.itemId) {
            R.id.nav_drive_layout -> {
                fragmentManager.beginTransaction().replace(R.id.content_frame, DriveFragment()).commit()
            }
            R.id.nav_select_layout -> {
                fragmentManager.beginTransaction().replace(R.id.content_frame, SelectFragment()).commit()
            }
            R.id.nav_options_layout -> {
                fragmentManager.beginTransaction().replace(R.id.content_frame, OptionsFragment()).commit()
            }
        }

        drawer_layout.closeDrawer(GravityCompat.START)
        return true
    }
}