package com.example.myapplication

import android.content.Context
import android.content.pm.PackageManager
import android.os.Bundle
import com.google.android.material.floatingactionbutton.FloatingActionButton
import com.google.android.material.snackbar.Snackbar
import androidx.appcompat.app.AppCompatActivity
import android.view.Menu
import android.view.MenuItem
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.GlobalScope
import kotlinx.coroutines.launch
import java.lang.Exception
import java.net.HttpURLConnection
import java.net.URL
import java.util.*
import javax.crypto.Cipher
import javax.crypto.KeyGenerator

fun ByteArray.toBase64(): String =
    String(Base64.getEncoder().encode(this))

fun String.fromBase64(): ByteArray =
    Base64.getDecoder().decode(this)

class MainActivity : AppCompatActivity() {

    val AES_IV = "8z9/AfEyGf46I5CNnO088A=="
    val AES_KEY = "1kXxu7EaYlPAY2do6DYQsqU1yL4p/f+s5DWB1/lOYIY="

    fun encrypt(context:Context, strToEncrypt: String): ByteArray {
        val plainText = strToEncrypt.toByteArray(Charsets.UTF_8)
        val keygen = KeyGenerator.getInstance("AES")
        keygen.init(256)
        val key = keygen.generateKey()
        val cipher = Cipher.getInstance("AES/CBC/NOPADDING")
        cipher.init(Cipher.ENCRYPT_MODE, key)

        val cipherText = cipher.doFinal(plainText)

        return cipherText
    }

    fun decrypt(context:Context, dataToDecrypt: ByteArray): ByteArray {
        println("not implemented")
        return ByteArray(0)
    }

    private fun getPlaintextFlagDispatcher() {
        GlobalScope.launch(Dispatchers.IO) {
            try {
                getPlaintextFlag()
            } catch (e: Exception) {
                println(e)
            }
        }
    }

    private fun getEncryptedFlagDispatcher() {
        GlobalScope.launch(Dispatchers.IO) {
            try {
                getEncryptedFlag()
            } catch (e: Exception) {
                println(e)
            }
        }
    }

    fun getPlaintextFlag() {
        val url = URL(
            "http://" +
                    "somnoynadno.ru:10006" +
                    "/api/plaintext_flag"
        )

        with(url.openConnection() as HttpURLConnection) {
            requestMethod = "GET"  // optional default is GET

            println("\nSent 'GET' request to URL : $url; Response Code : $responseCode")

            inputStream.bufferedReader().use {
                it.lines().forEach { line ->
                    println(line)
                }
            }
        }
    }

    fun getEncryptedFlag() {
        val url = URL(
            "http://" +
                    "somnoynadno.ru:10006" +
                    "/api/encrypted_flag"
        )

        with(url.openConnection() as HttpURLConnection) {
            requestMethod = "GET"  // optional default is GET

            println("\nSent 'GET' request to URL : $url; Response Code : $responseCode")

            var flag = ""
            inputStream.bufferedReader().use {
                it.lines().forEach { line ->
                    flag += line
                }
            }

            println("base64-flag is " + flag)
            println("TODO: add decryption")
        }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        setContentView(R.layout.activity_main)
        setSupportActionBar(findViewById(R.id.toolbar))

        // Here, thisActivity is the current activity
        if (ContextCompat.checkSelfPermission(this,
                android.Manifest.permission.INTERNET)
            != PackageManager.PERMISSION_GRANTED) {

            // Permission is not granted
            // Should we show an explanation?
            if (ActivityCompat.shouldShowRequestPermissionRationale(this,
                    android.Manifest.permission.INTERNET)) {
                // Show an explanation to the user *asynchronously* -- don't block
                // this thread waiting for the user's response! After the user
                // sees the explanation, try again to request the permission.
            } else {
                // No explanation needed, we can request the permission.
                ActivityCompat.requestPermissions(this,
                    arrayOf(android.Manifest.permission.INTERNET), 1)

                // REQUEST_CODE is an
                // app-defined int constant. The callback method gets the
                // result of the request.
            }
        } else {
            println("Permission is already granted")
        }

        findViewById<FloatingActionButton>(R.id.fab).setOnClickListener { view ->
            getPlaintextFlagDispatcher()
            Snackbar.make(view, "Скачал флаг для первого задания!", Snackbar.LENGTH_LONG)
                .setAction("Action", null).show()
        }

        findViewById<FloatingActionButton>(R.id.fab2).setOnClickListener { view ->
            getEncryptedFlagDispatcher()
            Snackbar.make(view, "Скачал зашифрованный флаг!", Snackbar.LENGTH_LONG)
                .setAction("Action", null).show()
        }
    }

    override fun onCreateOptionsMenu(menu: Menu): Boolean {
        // Inflate the menu; this adds items to the action bar if it is present.
        menuInflater.inflate(R.menu.menu_main, menu)
        return true
    }

    override fun onOptionsItemSelected(item: MenuItem): Boolean {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        return when (item.itemId) {
            R.id.action_settings -> true
            else -> super.onOptionsItemSelected(item)
        }
    }
}