package de.all4one_racingteam.all4onecontrol

import android.util.Log
import org.jetbrains.anko.doAsync
import java.io.*
import java.net.InetSocketAddress
import java.net.Socket
import java.net.SocketException
import java.net.UnknownHostException

class TcpClient (messageReceivedListener: OnMessageReceived, socketStatusChangedListener: OnSocketStatusChanged) {
    private var mServerMessage: String? = null
    private var mMessageListener: OnMessageReceived? = null
    private var mSocketStatusListener: OnSocketStatusChanged? = null
    private var mRun = false
    private var mRunning = false
    private var mConnecting = false
    private var mBufferOut: OutputStream? = null
    private var mBufferIn: BufferedReader? = null
    private var mServerAddress : InetSocketAddress? = null
    private var mToBeSendWhenConnected : ByteArray? = null

    init {
        mMessageListener = messageReceivedListener
        mSocketStatusListener = socketStatusChangedListener
    }

    fun sendMessage(message: ByteArray) {
        val runnable = Runnable {
            Log.d("TCP Client", "Sending: ${String(message)}")
            if (mBufferOut != null) {
                try {
                    mBufferOut!!.write(message)
                    mBufferOut!!.flush()
                } catch (e: SocketException){
                    Log.e("TCP Client", "Connection lost")
                    mToBeSendWhenConnected = message
                    Log.d("TCP Client", "Last message saved")
                    resetConnection()
                }
            }

        }
        val thread = Thread(runnable)
        thread.start()
    }

    fun sendMessage(message: String) {
        sendMessage(message.toByteArray())
    }

    fun stopClient() {
        mRun = false
        mRunning = false
        mConnecting = false
        if(mSocketStatusListener != null)
            mSocketStatusListener!!.socketDisconnected()
        Log.d("TCP Client", "S: Stopping...")

        if (mBufferOut != null) {
            mBufferOut!!.flush()
            mBufferOut!!.close()
        }
        mMessageListener = null
        mBufferIn = null
        mBufferOut = null
        mServerMessage = null
    }

    fun run(serverIP: String, serverPort: Int) {
        mServerAddress = InetSocketAddress(serverIP, serverPort)
        run()
    }

    fun run() {
        if (mServerAddress == null)
            return

        mRun = true
        try {
            Log.d("TCP Client", "C: Connecting...")

            val socket = Socket()
            try{
                mConnecting = true
                if(mSocketStatusListener != null)
                    mSocketStatusListener!!.socketConnecting()
                socket.connect(mServerAddress, 5000)

                onSocketConnected()

                mBufferOut = socket.getOutputStream()
                mBufferIn = BufferedReader(InputStreamReader(socket.getInputStream()))

                if(mToBeSendWhenConnected != null) {
                    Log.d("TCP Client", "sending Message in Buffer")
                    mBufferOut!!.write(mToBeSendWhenConnected)
                    mBufferOut!!.flush()
                    mToBeSendWhenConnected = null
                }


                while (mRun) {
                    mServerMessage = mBufferIn!!.readLine()

                    if (mServerMessage != null && mMessageListener != null) {
                        mMessageListener!!.messageReceived(mServerMessage!!)
                    }
                }
                Log.d("RESPONSE FROM SERVER", "S: Received Message: '$mServerMessage'")

            } catch (e: java.net.SocketTimeoutException){
                Log.d("TCP Client", "Timeout when trying to connect")
                stopClient()
            } catch (e: java.net.SocketException){
                when {
                    e.message == "Connection reset" -> {
                        Log.d("TCP Client", "Connection reset", e)
                        resetConnection()
                    }
                    e.message == "Socket closed" -> {
                        stopClient()
                    }
                    else -> {
                        Log.e("TCP Client", "Error", e)
                        stopClient()
                    }
                }
            } catch (e: UnknownHostException) {
                Log.e("TCP Client", "Unknown host", e)
                stopClient()
            }  catch (e: Exception) {
                Log.e("TCP Client", "S: Error", e)
                stopClient()
            } finally {
                socket.close()
            }

        } catch (e: Exception) {
            Log.e("TCP Client", "C: Error", e)
        }

    }

    private fun resetConnection (){
        Log.d("TCP Client", "Resetting Connection")
        stopClient()
        doAsync {
            run()
        }
    }

    private fun onSocketConnected (){
        Log.d("TCP Client", "C: Connected")
        mRunning = true
        mConnecting = false
        if(mSocketStatusListener != null)
            mSocketStatusListener!!.socketConnected()
    }

    fun isActive(): Boolean {
        return mRunning or mConnecting
    }

    interface OnMessageReceived {
        fun messageReceived(message: String)
    }

    interface OnSocketStatusChanged {
        fun socketConnected()
        fun socketDisconnected()
        fun socketConnecting()
    }

}

