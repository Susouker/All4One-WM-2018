package de.all4one_racingteam.all4onecontrol

import android.app.Application
import android.util.Log
import org.jetbrains.anko.doAsync

class GlobalState : Application(){

    private var mTcpClient: TcpClient? = null

    fun connectTcpClient(){
        Log.d("Global States", "trying to connect")
        doAsync {
            mTcpClient = TcpClient(object : TcpClient.OnMessageReceived {
                override fun messageReceived(message: String) {
                    Log.d("TCP Client", "Response: $message")
                }
            })
            mTcpClient!!.run("192.168.178.40", 14044)
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
