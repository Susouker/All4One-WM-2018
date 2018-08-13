package de.all4one_racingteam.all4onecontrol

import android.app.Application
import android.content.Context
import android.preference.PreferenceManager
import android.util.Log
import org.jetbrains.anko.doAsync

class GlobalState : Application(){

    private var mTcpClient: TcpClient? = null

    fun connectTcpClient(socketStatusListener : TcpClient.OnSocketStatusChanged){
        Log.d("Global States", "trying to connect")
        doAsync {
            mTcpClient = TcpClient(object : TcpClient.OnMessageReceived {
                override fun messageReceived(message: String) {
                    Log.d("TCP Client", "Response: $message")
                }
            }, socketStatusListener)

            val sharedPref = android.support.v7.preference.PreferenceManager.getDefaultSharedPreferences(applicationContext)
            val hostname = sharedPref.getString(SettingsActivity.hostnameKey, "localhost")
            val port =  sharedPref.getString(SettingsActivity.portKey, "14044").toInt()
            mTcpClient!!.run(hostname, port)
        }
    }

    fun disconnectTcpClient(){
        Log.d("Global States", "trying to disconnect")
        doAsync {
            if(isTcpClientConnected())
                mTcpClient!!.stopClient()
        }
    }

    fun isTcpClientConnected() : Boolean {
        return if(mTcpClient != null)
            mTcpClient!!.isActive()
        else
            false
    }

    fun sendTcpMessage(message: ByteArray){
        Log.d("Global States", "trying to send: " + message.toString())
        doAsync {
            if(isTcpClientConnected())
                mTcpClient!!.sendMessage(message)
        }
    }
}
