killall -q polybar

echo "---" | tee -a /tmp/polybar1.log /tmp/polybar2.log
polybar example >> /tmp/polybar1.log 2>&1 &
polybar par2 >> /tmp/polybar2.log 2>&1 &

echo "Bars launched..."
