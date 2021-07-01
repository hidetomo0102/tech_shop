# TECH SHOP
エンジニアなど、在宅でリモートワークをする人に向けたニッチなECサイトです。<br>
ユーザーはカスタマー（購買者）とサプライヤー（出品者）に分かれ、それぞれが独自のメニューを利用できる形です。<br>
レスポンシブ対応しているのでスマホやiPadからもご確認していただけます！<br>
<h3>ホーム画面</h3>
<img width="800" alt="TECH_SHOPホーム画面" src="https://user-images.githubusercontent.com/66961071/104279690-110dd180-54ee-11eb-9aed-92c931251cf7.png">
<h3>カスタマーログイン後の商品詳細画面</h3>
<img width="800" alt="カスタマートップ" src="https://user-images.githubusercontent.com/66961071/104279702-15d28580-54ee-11eb-9d77-71aee8a925fc.png">
（※決済ではStripeのデモコードとして「4242 4242 4242 4242(カード番号) 04/24(月/年) 242(CVC) 42424(ZIP)」が用意されていますのでご使用ください）
<h3>サプライヤートップ</h3>
<img width="800" alt="サプライヤートップ" src="https://user-images.githubusercontent.com/66961071/104279899-677b1000-54ee-11eb-9bbf-e56d19c8ef59.png">
（カスタマーの注文が入ったため、右上の『注文確認』ボタンに通知が来ています）
<br>

<h1>使用技術</h1>
<ul>
  <li>HTML/CSS</li>
  <li>Python3.7.9</li>
  <li>Django3.1.4</li>
  <li>MySQL 8.0.20</li>
  <li>Apache</li>
  <li>Docker/Docker-compose</li>
  <li>Bootstrap</li>
  <li>Stripe API（決済用）</li>
</ul>

<h1>インフラ</h1>
<ul>
  <li>AWS(Amazon Linux2 AMI)
  <ul>
    <li>VPC</li>
    <li>EC2</li>
    <li>RDS</li>
    <li>Route53</li>
    <li>S3（CSS配信/画像アップロード）</li>
  </ul>
  </li>
</ul>

<h1>機能一覧</h1>
<h3>□カスタマー側</h3>
<ul>
  <li>ユーザー登録、ログイン機能</li>
  <li>カート機能</li>
  <li>ほしい物リスト</li>
  <li>レビューコメント機能</li>
  <li>商品検索（キーワード/カテゴリー）</li>
  <li>Stripe APIを使用した決済機能</li>
</ul>
<h3>□サプライヤー側</h3>
<ul>
  <li>ユーザー登録、ログイン機能</li>
  <li>商品の出品機能（CRUD）</li>
  <li>自商品の購入通知機能</li>
</ul>
<h3>□全体</h3>
<ul>
  <li>レスポンシブデザイン</li>
  <li>ページネーション機能</li>
</ul>






