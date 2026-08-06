// 10-4절: 메뉴 아이콘 — 의존성 없는 인라인 SVG (지구본 모양)
import React from 'react';

export default function PortalIcon() {
    return (
        <svg
            width='20'
            height='20'
            viewBox='0 0 24 24'
            fill='none'
            stroke='currentColor'
            strokeWidth='2'
            strokeLinecap='round'
        >
            <circle cx='12' cy='12' r='9'/>
            <path d='M3 12h18'/>
            <path d='M12 3a13 13 0 0 1 0 18a13 13 0 0 1 0-18z'/>
        </svg>
    );
}
