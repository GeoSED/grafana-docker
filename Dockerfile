# Use the official Grafana image as the base
FROM grafana/grafana:latest

##################################################################
## CONFIGURATION
##################################################################

## Set Grafana options
ENV GF_ENABLE_GZIP=true
ENV GF_USERS_DEFAULT_THEME=light

USER root

## Replace Favicon and Apple Touch
COPY img/fav32.png /usr/share/grafana/public/img
COPY img/fav32.png /usr/share/grafana/public/img/apple-touch-icon.png

## Replace Logo
COPY img/grafana_icon.svg /usr/share/grafana/public/img/grafana_icon.svg

# Update Title
RUN sed -i 's|<title>\[\[.AppTitle\]\]</title>|<title>GeoSED Sensor System</title>|g' /usr/share/grafana/public/views/index.html
RUN sed -i 's|Loading Grafana|Loading GeoSED Sensor System|g' /usr/share/grafana/public/views/index.html

## Update Mega and Help menu
RUN sed -i "s|\[\[.NavTree\]\],|nav,|g; \
    s|window.grafanaBootData = {| \
    let nav = [[.NavTree]]; \
    const dashboards = nav.find((element) => element.id === 'dashboards/browse'); \
    if (dashboards) { dashboards['children'] = [];} \
    const connections = nav.find((element) => element.id === 'connections'); \
    if (connections) { connections['url'] = '/datasources'; connections['children'].shift(); } \
    const help = nav.find((element) => element.id === 'help'); \
    if (help) { help['subTitle'] = 'Business App 4.4.0'; help['children'] = [];} \
    window.grafanaBootData = {|g" \
    /usr/share/grafana/public/views/index.html

# Move Business App to navigation root section
RUN sed -i 's|\[navigation.app_sections\]|\[navigation.app_sections\]\nbusiness-app=root|g' /usr/share/grafana/conf/defaults.ini

##################################################################
## HANDS-ON
## Update JavaScript files
##################################################################

RUN find /usr/share/grafana/public/build/ -name *.js \
## Update Title
    -exec sed -i 's|AppTitle="Grafana"|AppTitle="GeoSED Sensor System"|g' {} \; \
## Update Login Title
    -exec sed -i 's|LoginTitle="Welcome to Grafana"|LoginTitle="GeoSED Sensor System"|g' {} \; \
## Remove Documentation, Support, Community in the Footer
    -exec sed -i 's|\[{target:"_blank",id:"documentation".*grafana_footer"}\]|\[\]|g' {} \; \
## Remove Edition in the Footer
    -exec sed -i 's|({target:"_blank",id:"license",.*licenseUrl})|()|g' {} \; \
## Remove Version in the Footer
    -exec sed -i 's|({target:"_blank",id:"version",text:f.versionString,url:D?"https://github.com/grafana/grafana/blob/main/CHANGELOG.md":void 0})|()|g' {} \; \
## Remove News icon
    -exec sed -i 's|(.,.....)(....,{className:.,onClick:.,iconOnly:!0,icon:"rss","aria-label":"News"})|null|g' {} \; \
## Remove Open Source icon
    -exec sed -i 's|.push({target:"_blank",id:"version",text:`${..edition}${.}`,url:..licenseUrl,icon:"external-link-alt"})||g' {} \;

