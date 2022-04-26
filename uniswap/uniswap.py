import os
import time
import logging
import functools
from typing import List, Any, Optional, Union, Tuple, Dict, Iterable

from web3 import Web3
from .types import AddressLike

from .util import (
    _str_to_addr,
    _addr_to_str,
    _validate_address,
    _load_contract,
    _load_contract_erc20,
    is_same_address,
)

from .constants import (
    _netid_to_name,
    _factory_contract_addresses_v1,
    _factory_contract_addresses_v2,
    _router_contract_addresses_v2,
    ETH_ADDRESS,
)

PROVIDER='https://mainnet.infura.io/v3/49d9273a4f5c446697ee32b9af8bc7cc'


logger = logging.getLogger(__name__)


class UniswapV3:
    """
    Wrapper around UniswapV3 contracts.
    """

    w3: Web3

    def __init__(
        self,
        address: Union[AddressLike, str, None],
        private_key: Optional[str],
        provider: str = None,
        use_estimate_gas: bool = True,
        network: str = 'ETHEREUM',
        web3: Web3 = None,
        non_fungible_manager_contract_addr: str = None
    ) -> None:
        """
        :param address: The public address of the ETH wallet to use.
        :param private_key: The private key of the ETH wallet to use.
        :param provider: Can be optionally set to a Web3 provider URI. If none set, will fall back to the PROVIDER environment variable, or web3 if set.
        :param web3: Can be optionally set to a custom Web3 instance.
        :param network: Can be optionally set to other chains.
        :param non_fungible_manager_contract_addr: Can be optionally set to override the address of the factory contract.
        """
        self.address = _str_to_addr(
            address or "0x0000000000000000000000000000000000000000"
        )
        self.private_key = (
            private_key
            or "0x0000000000000000000000000000000000000000000000000000000000000000"
        )

        if web3:
            self.w3 = web3
        else:
            # Initialize web3. Extra provider for testing.
            if not provider:
                provider = os.environ["PROVIDER"]
            self.w3 = Web3(Web3.HTTPProvider(PROVIDER, request_kwargs={"timeout": 60}))

        # Cache netid to avoid extra RPC calls
        self.netid = int(self.w3.net.version)
        if self.netid in _netid_to_name:
            self.netname = _netid_to_name[self.netid]
        else:
            raise Exception(f"Unknown netid: {self.netid}")
        logger.info(f"Using {self.w3} ('{self.netname}', netid: {self.netid})")

        # https://github.com/Uniswap/uniswap-v3-periphery/blob/main/deploys.md
        factory_contract_address = _str_to_addr(
            "0x1F98431c8aD98523631AE4a59f267346ea31F984"
        )
        self.factory_contract = _load_contract(
            self.w3, abi_name="uniswap-v3/factory", address=factory_contract_address
        )
        quoter_addr = _str_to_addr("0xb27308f9F90D607463bb33eA1BeBb41C27CE5AB6")
        self.router_address = _str_to_addr(
            "0xE592427A0AEce92De3Edee1F18E0157C05861564"
        )
        self.quoter = _load_contract(
            self.w3, abi_name="uniswap-v3/quoter", address=quoter_addr
        )
        self.router = _load_contract(
            self.w3, abi_name="uniswap-v3/router", address=self.router_address
        )
        non_fungible_manager_contract_addr = _str_to_addr(
            "0xC36442b4a4522E871399CD717aBDD847Ab11FE88"
        )
        self.non_fungible_manager = _load_contract(
            self.w3, abi_name="uniswap-v3/nonfungiblemanager", address=non_fungible_manager_contract_addr
        )

        # ------ NFT Manager --------------------------------------------------------------------

        def list_positions(self): 
            """
            async function NFTList(){
                const web3 = new Web3(provider);
                const acc = await web3.eth.getAccounts();
                var FROM = acc[0];
                var NFTLength = await TokBal(V3nftAddress);
                var nfts = [];
                for(var x=0;x<NFTLength;x++){
                    const V3NFT = new web3.eth.Contract(V3NFTabi,V3nftAddress);
                    var MyNFT = await V3NFT.methods.tokenOfOwnerByIndex(FROM,x).call({});
                    nfts.push('<a href="https://app.uniswap.org/#/pool/'+MyNFT+'" target="blank">https://app.uniswap.org/#/pool/'+MyNFT+'</a><br>');
                    document.getElementById("IDs").innerHTML = "looking..."
                }
                
                document.getElementById("IDs").innerHTML = nfts;
            }
            """
            # self.non_fungible_manager.functions
            return


        # ------ Market --------------------------------------------------------------------

if __name__ == "__main__":

    # Testing portion remove later
    testUni = UniswapV3()
    