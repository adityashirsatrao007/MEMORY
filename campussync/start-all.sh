#!/bin/bash

BASE_DIR="/home/aditya/Desktop/Projects/MEMORY"

echo "Starting all CampusSync variants..."

# Start Port 3002 (Original)
cd "$BASE_DIR/campussync" && nohup npm run dev > dev-server.log 2>&1 &
echo "Started base CampusSync on http://localhost:3002/"

# Start Port 3003 (Glassmorphism)
cd "$BASE_DIR/campussync-glass" && nohup npm run dev > dev-server.log 2>&1 &
echo "Started Glassmorphism variant on http://localhost:3003/"

# Start Port 3004 (Aurora Glow)
cd "$BASE_DIR/campussync-aurora" && nohup npm run dev > dev-server.log 2>&1 &
echo "Started Aurora Glow variant on http://localhost:3004/"

# Start Port 3005 (Neumorphism)
cd "$BASE_DIR/campussync-neumorph" && nohup npm run dev > dev-server.log 2>&1 &
echo "Started Neumorphism variant on http://localhost:3005/"

# Start Port 3006 (Neo-Brutalist)
cd "$BASE_DIR/campussync-brutalist" && nohup npm run dev > dev-server.log 2>&1 &
echo "Started Neo-Brutalist variant on http://localhost:3006/"

# Start Port 3007 (Claymorphism)
cd "$BASE_DIR/campussync-clay" && nohup npm run dev > dev-server.log 2>&1 &
echo "Started Claymorphism variant on http://localhost:3007/"

echo "All variants launched! Processes are running in the background."
