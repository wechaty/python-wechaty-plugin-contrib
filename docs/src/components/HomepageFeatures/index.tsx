import React from 'react';
import clsx from 'clsx';
import styles from './styles.module.css';

type FeatureItem = {
  title: string;
  Svg: React.ComponentType<React.ComponentProps<'svg'>>;
  description: JSX.Element;
};

const FeatureList: FeatureItem[] = [
  {
    title: 'Plugin System',
    Svg: require('@site/static/img/undraw_docusaurus_mountain.svg').default,
    description: (
      <>
        插件系统能够让开发者实现不同功能之间的完全隔离性。
        <br />
        高内聚，低耦合。
      </>
    ),
  },
  {
    title: 'Wechaty UI',
    Svg: require('@site/static/img/undraw_docusaurus_tree.svg').default,
    description: (
      <>
        新版本<code>Wechaty UI</code>能够让开发者用少量的代码即可开发出能够独立运行的UI界面，简单快速。
      </>
    ),
  },
  {
    title: 'Plugin Contrib',
    Svg: require('@site/static/img/undraw_docusaurus_react.svg').default,
    description: (
      <>
        插件库当中有很多官方支持和系统内置的插件列表，同时也欢迎各位开发者来贡献自己的插件。
      </>
    ),
  },
];

function Feature({title, Svg, description}: FeatureItem) {
  return (
    <div className={clsx('col col--4')}>
      <div className="text--center">
        <Svg className={styles.featureSvg} role="img" />
      </div>
      <div className="text--center padding-horiz--md">
        <h3>{title}</h3>
        <p>{description}</p>
      </div>
    </div>
  );
}

export default function HomepageFeatures(): JSX.Element {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}
