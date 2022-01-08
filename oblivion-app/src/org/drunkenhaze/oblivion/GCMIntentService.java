package org.drunkenhaze.oblivion;

import java.net.URLDecoder;

import org.apache.http.HttpEntity;
import org.apache.http.HttpResponse;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.impl.client.DefaultHttpClient;

import com.google.android.gcm.GCMBaseIntentService;

import android.app.Notification;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.content.Context;
import android.content.Intent;
import android.os.Vibrator;
import android.telephony.TelephonyManager;
import android.util.Log;

public class GCMIntentService extends GCMBaseIntentService {
	
	private static final String LOG_TAG = "Oblivion";
	private static final String SENDER_ID = "878778271728";
	private static final String PUSH_DATA_TITLE = "title";
	private static final String PUSH_DATA_MESSAGE = "message";
	
	public GCMIntentService() {
		super(SENDER_ID);
		if (BuildConfig.DEBUG)
			Log.d(LOG_TAG , "[GCMIntentService] start");
	}
	@Override
	protected void onError(Context context, String errorId) {
		if (BuildConfig.DEBUG)
			Log.d(LOG_TAG, "onError: " + errorId);
	}
	@Override
	protected void onMessage(Context context, Intent intent) {
		if (BuildConfig.DEBUG)
			Log.d(LOG_TAG, "GCMReceiver Message");
		try {
			String title = intent.getStringExtra(PUSH_DATA_TITLE);
			String message = URLDecoder.decode(intent.getStringExtra(PUSH_DATA_MESSAGE), "UTF-8");
			Vibrator vibrator = 
					(Vibrator) context.getSystemService(Context.VIBRATOR_SERVICE);
			vibrator.vibrate(1000);
			setNotification(context, title, message);
			if (BuildConfig.DEBUG)
				Log.d(LOG_TAG, title + ":" + message);
		} catch (Exception e) {
			Log.e(LOG_TAG, "[onMessage] Exception : " + e.getMessage());
		}
	}
	@Override
	protected void onRegistered(Context context, String regId) {
		Log.v(LOG_TAG, "onRegistered-registrationId = " + regId);
		// 3rd party 서버와 통신
		try {
			HttpClient client = new DefaultHttpClient();
			TelephonyManager mgr = (TelephonyManager)getSystemService(Context.TELEPHONY_SERVICE);
			String url = "http://oblivion.drunkenhaze.org/rest/register/" + regId + "/" + mgr.getLine1Number();
			HttpGet get = new HttpGet(url);
			client.execute(get);
		} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
	@Override
	protected void onUnregistered(Context context, String regId) {
		Log.v(LOG_TAG, "onUnregistered-registrationId");
		// 3rd party 서버와 통신
		try {
			HttpClient client = new DefaultHttpClient();
			String url = "http://oblivion.drunkenhaze.org/rest/unregister/" + regId;
			HttpGet get = new HttpGet(url);
			client.execute(get);
		} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
	private void setNotification(Context context, String title, String message) {
		NotificationManager notificationManager = null;
		Notification notification = null;
		try {
			notificationManager = (NotificationManager) context
					.getSystemService(Context.NOTIFICATION_SERVICE);
			notification = new Notification(R.drawable.ic_launcher,
					message, System.currentTimeMillis());
			Intent intent = new Intent(context, MainActivity.class);
			PendingIntent pi = PendingIntent.getActivity(context, 0, intent, 0);
			notification.setLatestEventInfo(context, title, message, pi);
			notificationManager.notify(0, notification);
		} catch (Exception e) {
			Log.e(LOG_TAG, "[setNotification] Exception : " + e.getMessage());
		}
	}
}
