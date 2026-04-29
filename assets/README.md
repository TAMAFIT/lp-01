# 差し替え画像の対応表

このLPは、元の8枚画像をデザインカンプとしてHTML/CSSで再構築した試作用です。
人物や施設写真は生成し直さず、後から実写真を配置できるように `data-photo` 名でスロット化しています。

使う画像をこの `assets` フォルダに入れたあと、`photos.css` の該当するコメント行を外すと差し替えできます。

主なスロット:

- `hero-trainers`: ファーストビューのトレーナー2名
- `counseling`: カウンセリング風景
- `training`: トレーニング風景
- `facility`: トレーニング機材
- `facility-wide`: 施設全体
- `machine`: 機材アップ
- `coach-support`: 指導風景
- `floor-support`: 床でのサポート風景
- `trainer-obayashi`: 大林トレーナー単体
- `trainer-tamai`: 玉井トレーナー単体
- `trainer-front`: 正面立ち姿
- `meal`: 食事サポート用の食事写真
- `line-reserve`: LINE予約の説明用写真
- `plan`: プラン提案の写真
- `final-counseling`: 最終ページ上部の相談写真
