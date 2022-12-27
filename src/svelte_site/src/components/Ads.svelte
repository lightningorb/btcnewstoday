<script type="text/javascript">
	import { base } from '$app/paths';
	import {
		Card,
		CardBody,
		CardFooter,
		CardHeader,
		CardSubtitle,
		CardText,
		CardTitle
	} from 'sveltestrap';
</script>

<Card>
	<CardBody>
		<CardSubtitle><b><p>Ads</p></b></CardSubtitle>
		<CardText>
			<p>
				<img
					alt="u"
					src="https://uploads-ssl.webflow.com/62966b49981ba146f4842f45/62966b49981ba1ae3c842f86_favicon.png"
					class="ad"
				/>&nbsp;&nbsp;<span class="ad-b"
					><a rel="noreferrer" target="_blank" href="https://umbrel.com/">Umbrel</a></span
				> — A personal server OS for self-hosting.
			</p>
			<p>
				<img alt="a" src="https://amboss.space/favicon.ico" class="ad" />&nbsp;&nbsp;<span
					class="ad-b"
					><a rel="noreferrer" target="_blank" href="https://amboss.space/">Amboss</a></span
				> — Lightning Network Power Tools #FindYourEdge.
			</p>
			<p>
				<img alt="g" src="{base}/geiser.png" class="ad" />&nbsp;&nbsp;<span class="ad-b"
					><a rel="noreferrer" target="_blank" href="https://geyser.fund/">Geyser Fund</a></span
				> — Lightning-native crowdfunding: Launch projects in just a few clicks.
			</p>
		</CardText>
	</CardBody>
</Card>
