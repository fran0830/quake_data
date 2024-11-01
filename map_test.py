import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

# 震源地の情報
latitude = 29.3
longitude = 130.4
hypocenter = "奄美大島北東沖"

# 図の作成
plt.figure(figsize=(10, 8))

# 地図投影の設定（PlateCarreeは地理座標系）
ax = plt.axes(projection=ccrs.PlateCarree())

# 世界地図の描画
ax.add_feature(cfeature.LAND)
ax.add_feature(cfeature.OCEAN)
ax.add_feature(cfeature.COASTLINE)
ax.add_feature(cfeature.BORDERS, linestyle=':')
ax.add_feature(cfeature.LAKES, alpha=0.5)
ax.add_feature(cfeature.RIVERS)

# 震源地のプロット
plt.plot(longitude, latitude, marker='*', color='red', markersize=15, transform=ccrs.PlateCarree())

# タイトルの設定
plt.title(f"震源地: {hypocenter}")

# 地図の範囲を設定（必要に応じて調整）
ax.set_extent([125, 140, 25, 35], crs=ccrs.PlateCarree())

# グリッド線の追加
ax.gridlines(draw_labels=True, dms=True, x_inline=False, y_inline=False)

# 画像として保存
plt.savefig('hypocenter_map.png', dpi=300, bbox_inches='tight')

print("震源地を地図にプロットし、'hypocenter_map.png'として保存しました。")
