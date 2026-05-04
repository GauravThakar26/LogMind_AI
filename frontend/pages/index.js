import { readFileSync } from 'fs';
import { join } from 'path';

export async function getServerSideProps() {
  const htmlContent = readFileSync(
    join(process.cwd(), 'public', 'index.html'),
    'utf8'
  );

  return {
    props: { htmlContent }
  };
}

export default function Home({ htmlContent }) {
  return (
    <div dangerouslySetInnerHTML={{ __html: htmlContent }} />
  );
}