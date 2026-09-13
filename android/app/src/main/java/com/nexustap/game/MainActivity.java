package com.nexustap.game;

import android.os.Bundle;
import android.view.WindowManager;

import androidx.core.view.WindowCompat;
import androidx.core.view.WindowInsetsCompat;
import androidx.core.view.WindowInsetsControllerCompat;

import com.getcapacitor.BridgeActivity;

public class MainActivity extends BridgeActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        // Keep screen on while playing
        getWindow().addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);

        // Draw edge to edge — required from Android 15 (API 35) on, where the system
        // no longer lets an app opt out of it.
        WindowCompat.setDecorFitsSystemWindows(getWindow(), false);
        applyImmersiveMode();
    }

    @Override
    public void onWindowFocusChanged(boolean hasFocus) {
        super.onWindowFocusChanged(hasFocus);
        // The system shows the bars again after a dialog, the keyboard or a task switch.
        if (hasFocus) {
            applyImmersiveMode();
        }
    }

    /**
     * Full-screen immersive mode via WindowInsetsController. Replaces the
     * SYSTEM_UI_FLAG_* constants, which are deprecated and ignored on modern Android.
     */
    private void applyImmersiveMode() {
        WindowInsetsControllerCompat controller =
                WindowCompat.getInsetsController(getWindow(), getWindow().getDecorView());
        controller.setSystemBarsBehavior(
                WindowInsetsControllerCompat.BEHAVIOR_SHOW_TRANSIENT_BARS_BY_SWIPE);
        controller.hide(WindowInsetsCompat.Type.systemBars());
    }
}
