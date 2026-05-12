*常用指令
进入虚拟环境
cd ~
python3 -m venv .ncatbot
. ~/.ncatbot/bin/activate
手动启动napcat
sudo xvfb-run -a /root/Napcat/opt/QQ/qq --no-sandbox -q 你的QQ号
首先构建docker
sudo docker build -t my-qqbot .

docker启动：sudo docker run -d \
  --name my-qqbot \
  --restart always \
  -p 6099:6099 \
  -w /app/bot \
  -v $(pwd)/data:/app/qqbot/data \
  -v $(pwd)/bot:/app/bot \
  --entrypoint sh \
  my-qqbot \
  -c "yes | python3 main.py"

检查状态/查看信息： docker logs -f napcat

* screen状态
记得使用参数scrren -r 来回到之前保存的窗口