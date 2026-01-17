% --- ELEVATION vs SLANT RANGE GRAFİK ÇİZİCİ ---

% 1. Parametreler (Senaryona göre)
Re = 6378.137; % Dünya Yarıçapı (km)
h = 600;       % Uydu İrtifası (km) - LEO
Rs = Re + h;

% 2. Açı Aralığı (0'dan 90 dereceye)
elev_deg = 0:0.1:90; 
elev_rad = deg2rad(elev_deg);

% 3. Slant Range Hesabı (Cosine Teoremi)
% d = Re * (sqrt((Rs/Re)^2 - cos^2(el)) - sin(el))
term1 = (Rs/Re)^2 - (cos(elev_rad)).^2;
d_km = Re * (sqrt(term1) - sin(elev_rad));

% 4. Grafiği Çiz ve Kaydet
figure('Color','w', 'Position', [100, 100, 800, 500]);
plot(elev_deg, d_km, 'LineWidth', 3, 'Color', [0.5, 0, 0.5]); % Mor renk
grid on;
box on;

% Eksen İsimleri (İngilizce - Makale İçin)
title('Slant Range vs. Elevation Angle', 'FontSize', 14, 'FontWeight', 'bold');
xlabel('Elevation Angle (deg)', 'FontSize', 12);
ylabel('Slant Range (km)', 'FontSize', 12);

% Kritik Noktaları İşaretle
text(0, d_km(1), sprintf('  Horizon: %.0f km', d_km(1)), ...
     'VerticalAlignment', 'bottom', 'FontSize', 10, 'FontWeight', 'bold');
text(90, d_km(end), sprintf('  Zenith: %.0f km', d_km(end)), ...
     'VerticalAlignment', 'bottom', 'HorizontalAlignment', 'right', 'FontSize', 10, 'FontWeight', 'bold');

% Dosyayı Kaydet
exportgraphics(gcf, 'elevation_vs_range.png', 'Resolution', 300);
disp('Grafik başarıyla kaydedildi: elevation_vs_range.png');