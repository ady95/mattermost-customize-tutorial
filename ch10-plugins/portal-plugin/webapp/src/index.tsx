// 10-4절: 진입점 — registerProduct 하나로 메뉴·라우트·메인 패널이 따라옵니다
import React from 'react';

import PortalIcon from './components/portal_icon';
import PortalView from './components/portal_view';
import manifest from './manifest';

const PORTAL_ROUTE = '/portal';

class PortalPlugin {
    initialize(registry: any) {
        registry.registerProduct(
            PORTAL_ROUTE,    // baseURL — 제품이 마운트될 라우트
            <PortalIcon/>,   // switcherIcon — 메뉴·헤더 아이콘
            '사내 포털',      // switcherText — 메뉴 표시 이름
            PORTAL_ROUTE,    // switcherLinkURL — 클릭 시 이동 경로
            PortalView,      // mainComponent — 메인 패널 컴포넌트
        );
    }
}

declare global {
    interface Window {
        registerPlugin(id: string, plugin: PortalPlugin): void;
    }
}

window.registerPlugin(manifest.id, new PortalPlugin());
