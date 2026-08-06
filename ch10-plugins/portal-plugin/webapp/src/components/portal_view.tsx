// 10-4절: 메인 패널 — 사내 서비스를 iframe으로 담습니다
import React from 'react';

const PORTAL_URL = 'https://portal.example.com/';

export default function PortalView() {
    return (
        <div style={{display: 'flex', width: '100%', height: '100%'}}>
            <iframe
                src={PORTAL_URL}
                title='사내 포털'
                style={{flex: 1, border: 'none',
                    backgroundColor: 'var(--center-channel-bg)'}}
                sandbox='allow-scripts allow-same-origin allow-forms allow-popups'
                referrerPolicy='no-referrer'
            />
        </div>
    );
}
