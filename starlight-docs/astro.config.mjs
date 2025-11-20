// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

// https://astro.build/config
export default defineConfig({

  integrations: [
    starlight({
      title: 'API RESTFull_Boletas',
      social: [{ icon: 'github', label: 'GitHub', href: 'https://github.com/luiyi45/API-RESTFull-Boletas.git' }],

      sidebar: [


        {
          label: 'Microservicios ',
          items: [
            {
              label: '1. Autenticación',
              link: '/auth/',
            },
            {
              label: '2. Categorias',
              link: '/categories/',
            },
            {
              label: '3. Ciudades',
              link: '/cities/',
            },
            {
              label: '4. Puntos de venta',
              link: '/points-of-sale/',
            },
          ],
        },

      ],
    }),
  ],

});
