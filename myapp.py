# practice python coding

""" from omegaconf import DictConfig, OmegaConf
import hydra

@hydra.main(version_base=None, config_path=".", config_name="config")
def my_app(cfg):
    print(OmegaConf.to_yaml(cfg)) """

def is_single(a):
    if a % 2 == 0:
        return False
    else:
        return True

if __name__ == "__main__":
    # my_app()
    a = input('Enter a:')
    a=int(a)
    if is_single(int(a)):
        print('{0}是奇数'.format(a))
        for i in range(10):
            print('{0:d}'.format(a+2*i))
    else:
        print('{0}是偶数'.format(a))
        for i in range(10):
            print('{0:d}'.format(a+2*i))